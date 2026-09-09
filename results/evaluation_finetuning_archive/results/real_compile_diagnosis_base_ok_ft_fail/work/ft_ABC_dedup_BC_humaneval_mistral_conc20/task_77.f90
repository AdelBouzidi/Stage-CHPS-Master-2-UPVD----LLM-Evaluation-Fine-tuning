program iscube_demo
  implicit none
  integer :: a
  logical :: result

  ! Read input from stdin
  read(*,*) a

  ! Call the iscube function
  result = iscube(a)

  ! Output the result
  print *, result
contains

  logical function iscube(a)
    implicit none
    integer, intent(in) :: a
    integer :: i

    do i = 1, 1000
      if (i*i*i == a) then
        iscube = .true.
        return
      end if
    end do
    iscube = .false.
  end function iscube

end program iscube_demo