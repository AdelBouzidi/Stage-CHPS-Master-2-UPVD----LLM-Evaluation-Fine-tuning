program iscube_demo
  implicit none
  integer :: a
  logical :: result

  ! Read input from stdin
  read *, a

  ! Call the iscube function
  result = iscube(a)

  ! Output the result
  print *, result

contains

  logical function iscube(a)
    implicit none
    integer, intent(in) :: a
    integer :: i

    iscube = .false.
    do i = 1, abs(a)
      if (i**3 == a) then
        iscube = .true.
        exit
      end if
    end do
  end function iscube

end program iscube_demo