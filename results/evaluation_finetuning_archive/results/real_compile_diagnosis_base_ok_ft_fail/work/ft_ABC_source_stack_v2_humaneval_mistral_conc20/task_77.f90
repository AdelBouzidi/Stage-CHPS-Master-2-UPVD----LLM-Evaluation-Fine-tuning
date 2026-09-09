program iscube_demo
  implicit none
  integer :: a
  logical :: result

  ! Hardcoded test input
  a = 1

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
    do i = 1, 1000
      if (i**3 == a) then
        iscube = .true.
        exit
      end if
    end do
  end function iscube

end program iscube_demo