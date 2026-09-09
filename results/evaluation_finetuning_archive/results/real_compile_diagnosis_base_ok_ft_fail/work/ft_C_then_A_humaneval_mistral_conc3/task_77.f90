program iscube_demo
  implicit none
  integer :: a
  logical :: result

  ! Read input
  read(*,*) a

  ! Call function
  result = iscube(a)

  ! Output result
  print *, result

contains

  logical function iscube(a)
    implicit none
    integer, intent(in) :: a
    integer :: i
    do i = 1, 1000
      if (i**3 == a) then
        iscube = .true.
        return
      end if
    end do
    iscube = .false.
  end function iscube

end program iscube_demo