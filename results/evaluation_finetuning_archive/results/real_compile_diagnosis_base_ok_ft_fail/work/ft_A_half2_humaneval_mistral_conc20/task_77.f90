program iscube_demo
  implicit none
  integer :: a
  logical :: result

  ! Read input
  read(*,*) a

  ! Call the function
  result = iscube(a)

  ! Output result
  print *, result

contains

  logical function iscube(a)
    implicit none
    integer, intent(in) :: a
    integer :: n
    logical :: found

    found = .false.
    do n = -100, 100
      if (n**3 == a) then
        found = .true.
        exit
      end if
    end do
    iscube = found
  end function iscube

end program iscube_demo